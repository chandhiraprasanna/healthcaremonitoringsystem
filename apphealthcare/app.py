from flask import Flask, render_template
from flask_socketio import SocketIO
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/varsini')
def index():
    return render_template('index.html')

@socketio.on('send_alert')
def handle_alert(data):
    data['time'] = datetime.now().strftime('%H:%M:%S')
    socketio.emit('receive_alert', data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
