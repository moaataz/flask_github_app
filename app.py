from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app,async_mode='gevent')

@socketio.on('connect')
def handle_connect(sid, environ):
    print(sid, 'connected')

@socketio.on('disconnect')
def handle_disconnect(sid):
    print(sid, 'disconnected')

if __name__ == '__main__':
    socketio.run(app)
