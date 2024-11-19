from app import create_app
from flask import request, abort
import subprocess
from app.db import db_blueprint
from app.user import user_blueprint
from app.ai import ai_blueprint
from app.speech import speech_blueprint
from app.speech.streaming_speech_to_text import socket_bp
from flask_socketio import SocketIO
from app.speech.streaming_speech_to_text import register_sockets

app, socketio = create_app()
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
register_sockets(socketio)
app.register_blueprint(db_blueprint)
app.register_blueprint(speech_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(ai_blueprint)
app.register_blueprint(socket_bp)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        subprocess.run(['./update_repo.sh'])
        return 'Updated', 200
    else:
        abort(400)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)