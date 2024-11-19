from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from .db.models import db

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tpd:tpd@samuelmoore.cc:5432/tpd'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
    
    return app, socketio
