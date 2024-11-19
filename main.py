from app import create_app
from flask import Flask, request, abort
import subprocess

app, socketio = create_app()

#test number 2

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Run the update script
        subprocess.run(['./update_repo.sh'])
        return 'Updated', 200
    else:
        abort(400)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)