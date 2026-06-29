from app.factory import socketio

@socketio.on('connect')
def handle_connect():
    print("Client is connected")