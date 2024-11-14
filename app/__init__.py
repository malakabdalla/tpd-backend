from flask import Flask
from flask_socketio import SocketIO
from app.socket_handler import init_socket_handlers  # Import the function to initialize socket events
from app.api import api_blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app)
    
    # Initialize SocketIO with app and CORS allowed origins
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

    app.register_blueprint(api_blueprint)
    
    # Initialize the socket handlers (pass the socketio instance to it)
    init_socket_handlers(socketio)

    return app, socketio
