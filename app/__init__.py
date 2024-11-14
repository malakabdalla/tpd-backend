from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from app.api import api_blueprint  
from app.socket_handler import SocketHandler 

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Register the API routes
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Initialize SocketIO
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

    # Attach the SocketHandler
    app.socketio = socketio

    return app, socketio
