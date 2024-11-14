from flask import Flask
from flask_socketio import SocketIO
from app.socket_handler import init_socket_handlers  # Import the function to initialize socket events

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

    # Initialize the socket handlers (pass the socketio instance)
    init_socket_handlers(socketio)

    return app, socketio
