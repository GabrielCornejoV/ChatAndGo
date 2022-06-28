from flask_app.controllers import routes
from flask_app import app
from flask import session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session

Session(app)
socketio = SocketIO(app, manage_session=False)
@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ', ha entrado en la sala.'}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ', ha salido de la sala.'}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
