from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from engine import NetworkEngine
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'noc_secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
engine = NetworkEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices')
def devices():
    return render_template('devices.html')

def background_monitoring():
    while True:
        stats = engine.get_stats()
        socketio.emit('network_update', stats)
        time.sleep(1)

if __name__ == '__main__':
    # Start monitoring thread
    threading.Thread(target=background_monitoring, daemon=True).start()
    socketio.run(app, debug=True, port=5000)
