from flask import Flask
from flask_socketio import SocketIO, send
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(msg):
    print(f"Mensagem recebida: {msg}")
    send(msg, broadcast=True)

def start_server():
    socketio.run(app, host="localhost", port=5000)

if __name__ == '__main__':
    start_server()
