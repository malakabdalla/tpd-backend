from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
# from app.api.questions import api_blueprint  # Import the blueprint
from app.socket_handler import init_socket_handlers  # Import socket handlers
from db.models import db
from db.questions import api_blueprint_get
from db.add_question import api_blueprint_add
from db.replace_question import api_blueprint_replace
from app.api import api_blueprint_speech


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tpd:tpd@samuelmoore.cc:5432/tpd'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    # Initialize extensions
    db.init_app(app)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
    
    # Register blueprints
    app.register_blueprint(api_blueprint_get)
    app.register_blueprint(api_blueprint_add)
    app.register_blueprint(api_blueprint_replace)
    app.register_blueprint(api_blueprint_speech)

    # Initialize socket handlers
    init_socket_handlers(socketio)

    return app, socketio
