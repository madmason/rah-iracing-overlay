from flask import Flask, render_template
from flask_socketio import SocketIO
from ir_telemetry import IRTelemetry
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
socketio = SocketIO(app)

telemetry = IRTelemetry(socketio)

@app.route('/')
def index():
    return render_template('overlay.html')

