from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
# from app.api.questions import api_blueprint  # Import the blueprint
from app.socket_handler import init_socket_handlers  # Import socket handlers
from .api.questions import api_blueprint

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri_here'  # Set your DB URI
    CORS(app)
    
    # Initialize extensions
    db.init_app(app)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
    
    # Register blueprints
    app.register_blueprint(api_blueprint)

    # Initialize socket handlers
    init_socket_handlers(socketio)

    return app, socketio
