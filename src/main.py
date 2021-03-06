from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .entities.entity import engine, Base
from .scheduler import scheduler
from .blueprints.bp_usuarios import bp_usuarios
from .blueprints.bp_autenticacion import bp_autenticacion
from .blueprints.bp_areasDeInteres import bp_areasDeInteres
from .blueprints.bp_files import bp_files
from .blueprints.bp_articulos import bp_articulos
from .blueprints.bp_personas import bp_personas


# creating the Flask application
app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'pagina_web_tcu_jwt_llave_secreta'
jwt = JWTManager(app)

# if needed, generate database schema
Base.metadata.create_all(engine)
scheduler.start()

app.register_blueprint(bp_usuarios)
app.register_blueprint(bp_autenticacion)
app.register_blueprint(bp_areasDeInteres)
app.register_blueprint(bp_files)
app.register_blueprint(bp_articulos)
app.register_blueprint(bp_personas)

