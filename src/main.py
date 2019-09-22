from flask import Flask
from flask_cors import CORS

from .entities.entity import engine, Base
from .blueprints.bp_usuarios import bp_usuarios

# creating the Flask application
app = Flask(__name__)
CORS(app)

# if needed, generate database schema
Base.metadata.create_all(engine)

app.register_blueprint(bp_usuarios)

