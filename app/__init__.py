from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from app.socket_handler import init_socket_handlers  # Import socket handlers
from .db.models import db
from .db import db_blueprint
from .user import user_blueprint
from .ai import ai_blueprint
from .speech import speech_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tpd:tpd@samuelmoore.cc:5432/tpd'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    # Initialize extensions
    db.init_app(app)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
    
    # Register blueprints
    app.register_blueprint(db_blueprint)
    app.register_blueprint(speech_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(ai_blueprint)

    # Initialize socket handlers
    init_socket_handlers(socketio)

    return app, socketio
