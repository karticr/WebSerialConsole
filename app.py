from flask import Flask, render_template
from flask_socketio import SocketIO

from libs.SerialController import SerialController

import json


bg_id = ""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
ASYNC_MODE = None
socketio = SocketIO(app, async_mode='threading', ping_timeout=30, logger=False, engineio_logger=False)

class socketHandler:
    def sendMsg(self, topic, msg):
        socketio.emit(topic, msg, room=bg_id)

sockets = socketHandler()
sc = SerialController(sockets)



@app.route('/')
def index():
    sc.writeToSerial("AT+CSQ")
    return render_template("page.html")

@app.route('/reset')
def reset():
    sc.reset()
    return render_template("page.html")

@app.route('/call')
def call():
    sc.writeToSerial("ATD9839905921")
    return "yolo"

@app.route('/hangup')
def hangup():
    sc.writeToSerial("ATH")
    return "yolo"

@app.route('/test')
def test():
    sc.writeToSerial("AT+CSQ")
    return "yolo"


@socketio.on('send')
def handle_send(data):
    print(data)

@socketio.on('serial_message')
def handle_send(msg):
    sc.writeToSerial(msg)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=False,  log_output=False)